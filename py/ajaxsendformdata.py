from flask import request, jsonify

@auth.route('/upload/', methods=['POST'])
@login_required
def upload():
    if request.method == 'POST':
        vcf_file = request.form['vcf_file']
        vcf_type = request.form['vcf_type']
        print(vcf_file)
        if vcf_file.filename == '':
            return jsonify({'msg': 'No selected file', 'table': []})

        if file and file.filename.rsplit('/')[-1][-6:] == 'vcf.gz':
            filename = secure_filename(file.filename)
            filepath = os.path.join(Config.VCF_FILE_PATH, current_user.username, filename)
            file.save(filepath)
            result = split_vcf(filepath)
            if result:
                return jsonify({'msg': 'ok', 'table': result})
        return jsonify({'msg': 'error'})
