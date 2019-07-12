from io import BytesIO

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageDraw, ImageFont


# ckeditor：给上传的图片添加水印
class WatermarkStorage(FileSystemStorage):
    # 重写save方法，添加水印
    def save(self, name, content, max_length=None):
        if 'image' in content.content_type:
            # 将文件对象转为图片对象，然后添加水印
            image = self.watermark_with_text(content, 'Master-Sun', 'red')
            # 再将图片对象转为文件对象
            content = self.convert_image_to_file(image, name)
        # 调用父类的save方法
        return super().save(name, content, max_length=max_length)

    def convert_image_to_file(self, image, name):
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = temp.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)

    # 字体参数fontfamily可指定本地字体文件路径
    def watermark_with_text(self, file_obj, text, color, fontfamily=None):
        image = Image.open(file_obj).convert('RGBA')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height / 20))
        else:
            font = None
        textWidth, textHeight = draw.textsize(text, font)
        x = (width - textWidth - margin) / 2    # 计算横轴位置
        y = (height - textHeight - margin)    # 设置纵轴位置
        draw.text((x, y), text, color, font)
        return image