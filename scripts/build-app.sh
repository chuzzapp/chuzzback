set -ex

git clone https://github.com/oursky/chuzz-app.git

cd app

npm install
npm run build

cd ..

mkdir -p public_html
mv app/www public_html/app
rm -rf app