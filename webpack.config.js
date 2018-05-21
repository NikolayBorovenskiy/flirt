let BowerWebpackPlugin = require("bower-webpack-plugin");
let webpack = require('webpack');
let autoprefixer = require('autoprefixer');


let webpackConfig = {
    context: __dirname,
    entry: {
        app: ['./assets/js/timetable.js'],
    },
    output: {
        filename: '[name].js',
        library: '[name]'
    },
    module: {
        preLoaders: [
            {
                test: /\.jsx?$/,
                loaders: ['eslint']
            }
        ],
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: [/node_modules/, /vendor/],
                loader: "babel-loader",
                query: {
                    plugins: ['transform-runtime'],
                    presets: ['es2015', 'react', 'stage-0']
                }
            },
            {
                test: /\.svg$/,
                loader: 'svg-inline'
            },
            {
                test: /\.scss$/,
                loader: 'style-loader!css-loader!sass-loader?sourceMap'
            },
            {
                test: /\.css$/,
                loader: "style-loader!css-loader"
            },
            {test: /jquery\.js$/, loader: 'expose?$'},
            {test: /jquery\.js$/, loader: 'expose?jQuery'}
        ],
        noParse: [
            new RegExp('.*vendor.*')
        ],
        postcss: [autoprefixer({browsers: ['>1%']})]
    },
    plugins: [
        new BowerWebpackPlugin({
            modulesDirectories: ["bower_components"],
            manifestFiles: "bower.json",
            includes: /.*/,
            excludes: [],
            searchResolveModulesDirectories: true
        }),
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            "window.jQuery": "jquery"
        })
    ]
};


let developmentConfig = Object.assign({}, webpackConfig, {
    watch: true,
    devtool: '#cheap-module-eval-source-map',
    plugins: webpackConfig.plugins.concat([
        new webpack.NoErrorsPlugin()
    ])
});


let productionConfig = Object.assign({}, webpackConfig, {
    output: {
        filename: '[name].min.js',
        library: '[name]'
    },
    plugins: webpackConfig.plugins.concat([
        // removes a lot of debugging code in React
        new webpack.DefinePlugin({
            'process.env': {
                'NODE_ENV': JSON.stringify('production')
            }
        }),
       // new webpack.optimize.OccurenceOrderPlugin(),
        new webpack.optimize.UglifyJsPlugin({compressor: {warnings: false}})
    ])
});


module.exports = {
    development: developmentConfig,
    production: productionConfig
};
