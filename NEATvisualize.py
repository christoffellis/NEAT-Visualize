import neat
import pygame


def draw_network(config: neat.Config, genome: neat.DefaultGenome, size: tuple, node_names: list[list[str]] = None,
                 show_disabled: bool = True,
                 colors: list[tuple[int, int, int]] = None,
                 save_file_name: str = None) -> pygame.Surface:
    """
    Draws a Neural Network given a NEAT-Python genome.


    :return:
    :rtype: pygame.Surface
    :param config: Config file
    :param genome: Agent genome
    :param size: Size of final output screen
    :param node_names: (Optional) [[Input Names], [Output Names]] Specifies the names
    :param show_disabled: (Optional) Show disabled nodes
    :param colors: (Optional) [(Positive Weight Color), (Negative Weight Color)]
    :param save_file_name: (Optional) file name for saving - no name defaults to not saving
    :return:
    """

    # Initial setup
    if colors is None:
        colors = [(255, 25, 25), (25, 255, 25)]

    screen = pygame.Surface(size, pygame.SRCALPHA, 32)
    screen = screen.convert_alpha()

    # Gather list of inputs, outputs and hidden nodes
    inputs = []
    for x, k in enumerate(config.genome_config.input_keys):
        inputs.append(str(k))

    outputs = []
    for x, k in enumerate(config.genome_config.output_keys):
        outputs.append(str(k))

    hidden_keys = []
    for n in genome.nodes.keys():
        if str(n) in inputs or str(n) in outputs:
            continue

        hidden_keys.append([str(n), 0])

    # Determine radius of circles to be drawn
    r = min(size[0] // 30, size[1] // 30, size[0] // (len(inputs) * 5), size[1] // (len(outputs) * 5))

    # Find maximum amount of hidden layers
    maxLayers = 0
    if len(hidden_keys) > 0:
        for x in range(len(hidden_keys)):
            hidden_keys[x][1] = get_dependency_count(hidden_keys[x], genome, outputs, hidden_keys, show_disabled)
            maxLayers = max(maxLayers, hidden_keys[x][1])

    # Clear all unused input nodes if we don't draw disabled connections
    if not show_disabled:
        allInputNodes = []
        for cg in genome.connections.values():
            if cg.enabled or show_disabled:
                input, output = cg.key
                allInputNodes.append(str(input))

        inputs = list(set(inputs).intersection(allInputNodes))

    # Draw all connections
    for cg in genome.connections.values():
        if cg.enabled or show_disabled:
            input, output = cg.key
            a = str(input)
            b = str(output)

            color = color_mix(colors, cg.weight) if cg.enabled else 'gray'

            aPos = get_position(a, inputs, outputs, hidden_keys, size, r, maxLayers)
            bPos = get_position(b, inputs, outputs, hidden_keys, size, r, maxLayers)

            pygame.draw.aaline(screen, color, aPos, bPos)  # , width=int(width))

    # Draw input, output and hidden nodes
    offset = size[1] // len(inputs)
    for x in range(len(inputs)):
        pygame.draw.circle(screen, (255, 255, 255), (r, offset * x + offset // 2), r)
        if node_names is not None:
            writeText(screen, node_names[0][x], 0, offset * x + offset // 2 - r * 1.2, (255, 255, 255), True)

    offset = size[1] // len(config.genome_config.output_keys)
    for x in range(len(outputs)):
        pygame.draw.circle(screen, (255, 255, 255), (size[0] - r, offset * x + offset // 2), r)

    if len(hidden_keys) > 0:
        offsetY = size[1] // len(hidden_keys)

        offsetX = size[0] // (maxLayers + 1)

        for x, k in enumerate(hidden_keys):
            pygame.draw.circle(screen, (255, 255, 255), ((maxLayers + 1 - k[1]) * offsetX, offsetY * x + offsetY // 2),
                               r)

    # Save neural network to image if save_file_name is specified
    if not (save_file_name is None):
        pygame.image.save(screen, save_file_name)

    # Finally returns the screen
    return screen


def get_dependency_count(id, genome, outputs, hidden, show_disabled):
    maxOut = 0
    for cg in genome.connections.values():
        if cg.enabled or show_disabled:
            inputted, output = cg.key
            if id[0] == str(inputted):
                if str(output) in outputs:
                    maxOut = max(1, maxOut)
                else:
                    maxOut = max(get_dependency_count([str(output), 0], genome, outputs, hidden, show_disabled) + 1,
                                 maxOut)
    return maxOut


def get_position(key, inputs, outputs, hidden, size, r, maxLayers):
    if key in inputs:
        offset = size[1] // len(inputs)
        return (r, offset * inputs.index(key) + offset // 2)

    if key in outputs:
        offset = size[1] // len(outputs)
        return (size[0] - r, offset * outputs.index(key) + offset // 2)

    for x, k in enumerate(hidden):
        if key == k[0]:
            offsetY = size[1] // len(hidden)
            offsetX = size[0] // (maxLayers + 1)

            return ((maxLayers + 1 - k[1]) * offsetX, offsetY * x + offsetY // 2)


def writeText(screen, string, coordx, coordy, colour, center=True, background=None):
    # set the font to write with
    font = pygame.font.SysFont('calibri', 10)
    if background == None:
        # (0, 0, 0) is black, to make black text
        text = font.render(string, True, colour)
    else:
        text = font.render(string, True, colour, background)
    # get the rect of the text
    textRect = text.get_rect()
    # set the position of the text
    if center:
        textRect.bottomleft = (coordx, coordy)
    else:
        textRect.topleft = (coordx, coordy)
    screen.blit(text, textRect)


def clamp(val):
    return min(1, max(val, 0))


def color_mix(colors, weight):
    return [
        (colors[0][0] * clamp(weight / 4) + colors[1][0] * (1 - clamp(weight / 4))),
        (colors[0][1] * clamp(weight / 4) + colors[1][1] * (1 - clamp(weight / 4))),
        (colors[0][2] * clamp(weight / 4) + colors[1][2] * (1 - clamp(weight / 4))),
    ]
