import pygame


def drawNetwork(config, genome, size, node_names=None, node_colors=None, show_disabled=True):
    screen = pygame.Surface((size))

    if node_names is None:
        node_names = {}

    assert type(node_names) is dict

    if node_colors is None:
        node_colors = {}

    assert type(node_colors) is dict


    r = min(size[0] // 20, size[1] // 20)

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

        hidden_keys.append(str(n))

    for cg in genome.connections.values():
        if cg.enabled or show_disabled:
            input, output = cg.key
            a = node_names.get(input, str(input))
            b = node_names.get(output, str(output))
            color = 'green' if cg.weight > 0 else 'red' if cg.enabled else 'gray'
            width = 1 + abs(cg.weight)
            aPos = get_position(a, inputs, outputs, hidden_keys, size, r)
            bPos = get_position(b, inputs, outputs, hidden_keys, size, r)

            pygame.draw.line(screen, color, aPos, bPos, width=int(width))

    offset = size[1] // len(config.genome_config.input_keys)
    for x in range(len(inputs)):
        pygame.draw.circle(screen, (255, 255, 255), (r, offset * x + offset // 2), r)

    offset = size[1] // len (config.genome_config.output_keys)
    for x in range(len(outputs)):
        pygame.draw.circle(screen, (255, 255, 255), (size[0]-r, offset * x + offset // 2), r)

    if len(hidden_keys) > 0:
        offset = size[1] // len(hidden_keys)
        for x, k in enumerate(hidden_keys):
            pygame.draw.circle(screen, (255, 255, 255), (size[0] // 2, offset * x + offset // 2), r)

    return screen


def get_position(key, inputs, outputs, hidden, size, r):
    if key in inputs:
        offset = size[1] // len(inputs)
        return (r, offset * inputs.index(key) + offset // 2)

    if key in outputs:
        offset = size[1] // len(outputs)
        return (size[0] - r, offset * outputs.index(key) + offset // 2)

    if key in hidden:
        offset = size[1] // len(hidden)
        return (size[0] // 2, offset * hidden.index(key) + offset // 2)
