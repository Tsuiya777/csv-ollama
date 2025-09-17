# ベースイメージとして軽量なNginxを使用
FROM nginx:alpine

# HTMLファイルをNginxの公開ディレクトリへコピー
COPY ./html /usr/share/nginx/html

# nginxの設定ファイルをコピー
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# コンテナが公開するポート番号
EXPOSE 80

# デフォルトのNginxエントリーポイントを使用
