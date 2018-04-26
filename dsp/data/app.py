# coding:utf-8
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

def upload_routes(app):
    @app.route('/api/upload/put', methods=['POST'])
    def upload():
        print 'haha'
        #if request.method == 'POST':
        f = request.files['file']
        print f.filename
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'templates/uploads',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        #return redirect(url_for('upload'))
        return '上传成功'

    @app.route('/api/upload/get', methods=['GET'])
    def upload_get():
        print 'haha'
        #return redirect(url_for('upload.html'))
        return render_template('upload.html')
# if __name__ == '__main__':
#     app.run('0.0.0.0', 61, debug=True, use_reloader=True)