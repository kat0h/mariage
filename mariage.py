from PIL import Image


def num2tenjicode(num: int):
    flags = 0
    flags += (num & 0b00001000) << 3
    flags += (num & 0b01110000) >> 1
    flags += (num & 0b10000111)
    return chr(flags + 0x2800)


def image2tenji(image: list):
    # リストのサイズを調節
    # (x, y)
    size = [len(image), len(image[0])]
    size2 = [
        (size[0] // 4 + size[0] % 4) * 4,
        (size[1] // 2 + size[1] % 2) * 2,
    ]
    image2 = [[0] * size2[1] for i in range(size2[0])]
    for i in range(size[0]):
        for j in range(size[1]):
            image2[i][j] = image[i][j]
    # 点字化
    ret = ""
    for i in range(0, size2[0], 4):
        for j in range(0, size2[1], 2):
            code = 0
            code += image2[i][j] * 1
            code += image2[i+1][j] * 2
            code += image2[i+2][j] * 4
            code += image2[i+3][j] * 8
            code += image2[i][j+1] * 16
            code += image2[i+1][j+1] * 32
            code += image2[i+2][j+1] * 64
            code += image2[i+3][j+1] * 128
            ret += num2tenjicode(code)
        ret += "\n"
    return ret[0:-1]


if __name__ == "__main__":
    # Image PATH
    im = Image.open("./mariage.jpg")
    # Image size
    im = im.resize((im.width // 1, im.height // 1)).convert('L')
    limg = []
    for i in range(im.height):
        k = []
        for j in range(im.width):
            pixel = (not im.getpixel((j, i)) > 128) * 1
            k.append(pixel)
        limg.append(k)
    print(image2tenji(limg))
