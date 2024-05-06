module.exports = {
  presets: [
    ['@babel/preset-flow', {
      targets: {
        node: 'current', // Target the current version of Node
      }
    }],
    '@babel/preset-react' // Add this to handle JSX
  ],
};
