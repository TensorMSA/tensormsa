var path = require('path');
var webpack = require('webpack');

var envPlugin = new webpack.DefinePlugin({
    // __API_SERVER__: "http://localhost:8989"//JSON.stringify(process.env.API_SERVER)
});

module.exports = {
    entry: {
        TensorMSA: './js/app.js'
    }, // Multiple Entry
    devtool: 'sourcemaps',
    cache: true,
    debug: true,
    output: {
        path: __dirname,
        filename: './../static/dist/[name].js' // Output for the multiple entry
    },
    resolve: {
        // Add `.ts` and `.tsx` as a resolvable extension. 
        extensions: ['', '.webpack.js', '.web.js', '.js', '.jsx']
    },  
    // When to use Minification, 
    plugins : [
        envPlugin
        //new webpack.optimize.UglifyJsPlugin()
    ],
    module: { // An array of extensions that should be used to resolve modules.
        loaders: [
            { 
                test: /\.jsx?$/,         // Match both .js and .jsx files
                exclude: /node_modules/, 
                loader: "babel",
                query:
                {
                    presets:['es2015','react']
                }
            },
            {
                test: /\.css$/, 
                loader: "style-loader!css-loader"
            },
            {
                test: /\.scss$/,
                loader: "style-loader!css-loader!sass-loader"
            },
            {
                test: /\.png$/,
                loader: "url-loader"
            }
            ,
            {
                test: /\.jpg$/,
                loader: "url-loader"
            }
        ]
    },

    node: {
        fs: "empty"
    }
};
