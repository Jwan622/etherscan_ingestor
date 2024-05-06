import React, { useState } from 'react';
import styles from './DualFieldSearchBar.module.css';

const DualFieldSearchBar = ({ onSubmit }) => {
  const [address, setAddress] = useState('');
  const [timestamp, setTimestamp] = useState('');

  const handleChange = (setter) => (event) => {
    setter(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (address && timestamp) {
      onSubmit({ address, timestamp });
    } else if (address) {
      onSubmit({ address });
    } else if (timestamp) {
      onSubmit({ timestamp });
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.formContainer}>
      <input
        type="text"
        placeholder="Search by address"
        value={address}
        onChange={handleChange(setAddress)}
        className={styles.searchInput}
      />
      <input
        type="text"
        placeholder="Search by date (YYYY-MM-DD HH:MM:SS)"
        value={timestamp}
        onChange={handleChange(setTimestamp)}
        className={styles.searchInput}
      />
      <button type="submit" className={styles.searchButton} disabled={!address && !timestamp}>
        Search
      </button>
    </form>
  );
};

export default DualFieldSearchBar;
