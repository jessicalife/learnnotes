from flask import Flask, render_template, jsonify, request
import pandas as pd
import py1
import py2
import py3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    # 获取前端发来的数据
    script_id = request.json.get('id')
    user_input = request.json.get('audit_id') 
    
    try:
        # 根据按下的按钮，调用不同的 python 脚本
        if script_id == 1:
            result_df = py1.run(user_input)
        elif script_id == 2:
            result_df = py2.run(user_input)
        elif script_id == 3:
            result_df = py3.run(user_input)
        else:
            return jsonify({"error": "Invalid script ID"}), 400

        # 如果没有找到数据，返回一个提示
        if result_df.empty:
            return jsonify([{"Message": f"No data found for input: {user_input}"}])

        # 将 DataFrame 转换为字典列表，方便前端表格显示
        # fillna('') 是为了防止 excel 里的空值 (NaN) 导致 JSON 报错
        result_data = result_df.fillna('').to_dict(orient='records')
        return jsonify(result_data)

    except Exception as e:
        # 如果读取出错（比如文件没找到），把错误信息发给前端
        return jsonify([{"Error": str(e)}])

# 读取顶部的两个完整文件作展示
@app.route('/get_source_data', methods=['GET'])
def get_source_data():
    source = request.args.get('source')
    try:
        if source == 'qcp2':
            df = pd.read_excel('QC Part2.xlsx')
        else:
            df = pd.read_excel('Network Table.xlsx')
        return jsonify(df.fillna('').to_dict(orient='records'))
    except Exception as e:
         return jsonify([{"Error": str(e)}])

from flask import Flask, render_template, jsonify, request, send_file
import pandas as pd
import io
import py1
import py2
import py3

# ... (你之前的 app = Flask(__name__) 和其他路由代码保持不变) ...

@app.route('/export', methods=['POST'])
def export_excel():
    # 1. 接收前端发来的当前表格数据 (JSON 格式)
    table_data = request.json
    
    if not table_data or len(table_data) == 0:
        return jsonify({"error": "No data to export"}), 400

    # 2. 把 JSON 数据转回 pandas DataFrame
    df = pd.DataFrame(table_data)

    # 3. 在内存中创建一个 Excel 文件（不需要在电脑上生成实体文件）
    output = io.BytesIO()
    # 使用 openpyxl 引擎写入 Excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Exported Results')
    
    # 4. 把内存指针移回文件开头，准备发送
    output.seek(0)

    # 5. 把 Excel 文件发送给前端浏览器触发下载
    return send_file(
        output,
        as_attachment=True,
        download_name='Audit_Network_Result.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == '__main__':
    app.run(debug=True)
