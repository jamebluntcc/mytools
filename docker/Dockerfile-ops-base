from python:3.6.10-alpine
RUN sed -i 's/dl-cdn.alpinelinux.org/mirror.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
run apk add --no-cache --virtual=build-dependencies \
    g++ \
    build-base libffi-dev \
    libffi openssl ca-certificates \
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    linux-headers pcre-dev
env wd=/requirements
add ./requirements/dev.txt ${wd}/dev.txt
run pip install -i https://pypi.douban.com/simple -r ${wd}/dev.txt && rm -rf ${wd}




