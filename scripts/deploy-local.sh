set -ex

cd cms/client
npm install
npm run build
cd ../..

rm -rf public_html
mv cms/client/build public_html
cp cms-config.yaml public_html

mv cms/client ..
mv env ..

skycli deploy

mv ../env env
mv ../client cms
