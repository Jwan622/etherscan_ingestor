module.exports = {
  setupFilesAfterEnv: ['@testing-library/jest-dom/extend-expect'],
  testEnvironment: 'jsdom', // important for testing components that interact with the DOM
  testPathIgnorePatterns: ['/node_modules/', '/.next/'],
  transform: {
    // Use babel-jest to transform JS and JSX files
    '^.+\\.(js|jsx|ts|tsx)$': '<rootDir>/node_modules/babel-jest',
  },
  moduleNameMapper: {
    // Mock static assets
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy'
  }
};
