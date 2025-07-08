from PIL import Image
import freetype
from cf_wrapper import Config


class BitmapFontGenerator:
    def __init__(self, config: Config):
        self.pixel_size = config.get("font_settings/pixel_size")
        self.mono_spaced = config.get("font_settings/mono_spaced")

        self.equal_character_spacing = config.get("export_settings/equal_character_spacing")
        self.texture_size_w = config.get("export_settings/texture_size_w")
        self.texture_size_h = config.get("export_settings/texture_size_h")
        self.compress_level = config.get("export_settings/compress_level")
        self.padding_x = config.get("export_settings/padding_x")
        self.padding_y = config.get("export_settings/padding_y")

        self.chars = [chr(i) for i in range(32, 127)]


    def ttf_to_fnt(self, fontfile, output_name):
        self.fnt_data = []
        self._initialize_image()
        self._initialize_face(fontfile)
        self._initialize_sizes()

        self._generate_image(output_name)
        self._generate_fnt(output_name)
        print(f"Saved {output_name}.png and {output_name}.fnt")


    def _generate_image(self, output_name):
        ascender = self.face.size.ascender >> 6
        cursor_x = cursor_y = 0

        for _, ch in enumerate(self.chars):
            self.face.load_char(ch)
            bitmap = self.face.glyph.bitmap
            top = self.face.glyph.bitmap_top
            left = self.face.glyph.bitmap_left

            glyph_w, glyph_h = bitmap.width, bitmap.rows
            glyph_image = self._render_glyph_image(bitmap)
            width = self.max_width if self.equal_character_spacing else glyph_w
            height = glyph_h

            if cursor_x + width + self.padding_x > self.texture_size_w:
                cursor_x = 0
                cursor_y += self.line_height + self.padding_y
            
            baseline_y = cursor_y + ascender
            paste_y = baseline_y - top

            self.image.paste(glyph_image, (cursor_x, paste_y))
            self.fnt_data.append(Glyph(
                char=ch,
                x=cursor_x,
                y=paste_y,
                width=width,
                height=height,
                xoffset=left,
                yoffset=ascender - top,
                xadvance= self.max_width if self.mono_spaced else self.face.glyph.advance.x >> 6,
            ))

            cursor_x += self.max_width + self.padding_x if self.mono_spaced else width + self.padding_x

        compress_level = clamp(self.compress_level, 0, 9)
        self.image.save(f"{output_name}.png", compress_level=compress_level)


    def _generate_fnt(self, output_name):
        with open(f"{output_name}.fnt", "w") as f:
            f.write("info face=\"custom\" size=%d\n" % self.pixel_size)
            f.write(f"common lineHeight={self.line_height} base={self.pixel_size} scaleW={self.texture_size_w} scaleH={self.texture_size_h} pages=1 packed=0\n")
            f.write("page id=0 file=\"%s.png\"\n" % output_name)
            f.write("chars count=%d\n" % len(self.fnt_data))

            for g in self.fnt_data:
                f.write(g.to_fnt_string())
    

    def _initialize_image(self):
        self.image = Image.new("L", (self.texture_size_w, self.texture_size_h), 0)

    def _initialize_face(self, fontfile):
        self.face = freetype.Face(fontfile)
        self.face.set_pixel_sizes(0, self.pixel_size)


    def _initialize_sizes(self):
        (self.max_width, self.max_height) = self._get_max_width_and_height()
        self.line_height = self.max_height + self.padding_y


    def _render_glyph_image(self, bitmap):
        return Image.frombytes("L", (bitmap.width, bitmap.rows), bytes(bitmap.buffer))


    def _get_max_width_and_height(self) -> tuple:
        max_width = max_height = 0
        render_mode = self._get_render_mode()

        for ch in self.chars:
            self.face.load_char(ch, render_mode)
            bitmap = self.face.glyph.bitmap
            max_width = max(max_width, bitmap.width)
            max_height = max(max_height, bitmap.rows)

        return (max_width, max_height)


    def _get_render_mode(self):
        return freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL
        

class Glyph:
    def __init__(self, char, x, y, width, height, xoffset, yoffset, xadvance):
        self.id = ord(char)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.xadvance = xadvance
        self.letter = char
    
    
    def to_fnt_string(self):
        return f"char id={self.id:<5}   x={self.x:<5}     y={self.y:<5}     width={self.width:<5}     height={self.height:<5}      xoffset={self.xoffset:<5}     yoffset={self.yoffset:<5}     xadvance={self.xadvance:<5}     page=0  chnl=0\n"


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))