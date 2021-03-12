const path = require('path');


module.exports = {
  entry: {
    index: './assets/index.js',
    moduleParse: './assets/moduleParse.js'
  },  // path to our input file
  output: {
    filename: '[name].bundle.js',  // output bundle file name
    path: path.resolve(__dirname, './static'),  // path to our Django static directory
    library: '[name]'
  },
  module: {
    rules: [
      {
        test: /\.(js)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: { presets: ["@babel/preset-env"] }
      },
      {
        test: /\.css$/i,
        // exclude: /node_modules/,
        use: ['style-loader', "css-loader"],
      }
    ]
  }
};