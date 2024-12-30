import os
from flask import Flask, request, jsonify, send_from_directory
import yt_dlp

app = Flask(__name__)

# ダウンロード先ディレクトリ
DOWNLOAD_FOLDER = "/tmp/downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# yt-dlp設定
ydl_opts = {
    'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # 保存先パスの設定
    'format': 'best',  # 最適なフォーマットを選択
    'quiet': True,  # 出力を抑制
    'noplaylist': True  # プレイリストのダウンロードを防止
}

@app.route('/api/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    # yt-dlpで動画をダウンロード
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 動画の情報を取得し、ダウンロード
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', 'Unknown title')
            video_ext = info_dict.get('ext', 'mp4')  # 拡張子（例：mp4）
            download_path = os.path.join(DOWNLOAD_FOLDER, f"{video_title}.{video_ext}")
            
            # ダウンロード後にファイルパスを返す
            return jsonify({'download_link': f'/downloads/{video_title}.{video_ext}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/downloads/<filename>')
def serve_file(filename):
    # ダウンロードしたファイルを提供するエンドポイント
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
