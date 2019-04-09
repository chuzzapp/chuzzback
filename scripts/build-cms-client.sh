set -ex

git submodule update --init --recursive

cd cms/client

if [ -f ../../cms-config/.env ]; then 
  mv ../../cms-config/.env ./.env;
fi

npm install
npm run build

cd ../..

mkdir -p public_html
mv cms/client/build public_html/cms
cp cms-config.yaml public_html/cms
rm -rf cms/client
