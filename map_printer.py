from PIL import Image, ImageDraw

with Image.open('tree.png') as im:
    tree_png = im.convert('RGBA')
with Image.open('dark.png') as im:
    dark_png = im.convert('RGBA')
with Image.open('fire.png') as im:
    fire_png = im.convert('RGBA')
with Image.open('item.png') as im:
    item_png = im.convert('RGBA')
with Image.open('bomb.png') as im:
    bomb_png = im.convert('RGBA')
with Image.open('path.png') as im:
    path_png = im.convert('RGBA')
with Image.open('bobb.png') as im:
    bobb_png = im.convert('RGBA')
with Image.open('mark.png') as im:
    mark_png = im.convert('RGBA')
img_dict = {
    '树': tree_png,
    '黑': dark_png,
    '熔': fire_png,
    '箱': item_png,
    '裂': bomb_png,
    '路': path_png,
    '商': bobb_png,
    '问': mark_png,
}


def map_printer(file):
    with open(file + '.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        max_x = len(lines[0]) - 1
        max_y = len(lines)
    max_width = max_x * 25
    max_height = max_y * 25
    image = Image.new('RGB', (max_width, max_height), color='white')
    draw = ImageDraw.Draw(image)
    for i in range(max_x):
        draw.line([(i * 25 - 1, -1), (i * 25 - 1, max_height - 1)], fill='black', width=2)
    for i in range(max_y + 1):
        draw.line([(-1, i * 25 - 1), (max_width - 1, i * 25 - 1)], fill='black', width=2)
    for y in range(max_y):
        line = lines[y]
        y_pix = y * 25
        for x in range(max_x):
            x_pix = x * 25
            char = line[x]
            if char == '墙':
                draw.rectangle([(x_pix, y_pix), (x_pix + 25, y_pix + 25)], fill='black')
            elif char == '空' or char == '起':
                pass
            else:
                tile_png = img_dict[char]
                image.paste(tile_png, (x_pix, y_pix), tile_png)
    image.save(file + '.png')


if __name__ == '__main__':
    map_printer('map1')
    map_printer('map2')
    map_printer('map3')
    map_printer('map4')
    map_printer('map5')
    map_printer('map6')
