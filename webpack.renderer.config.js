const rules = require('./webpack.rules');
const path = require('path');

rules.push(
  {
    test: /\.css$/,
    use: [{ loader: 'style-loader' }, { loader: 'css-loader' }],
  },
  {
    test: /\.(png|jpe?g|gif|svg)$/i,
    type: 'asset/resource'
  }
);

module.exports = {
  // Put your normal webpack config below here
  module: {
    rules,
  },
  resolve: {
    extensions: ['.js', '.json', '.css'],
  },
  output: {
    assetModuleFilename: 'assets/[name][ext]'
  }
};
