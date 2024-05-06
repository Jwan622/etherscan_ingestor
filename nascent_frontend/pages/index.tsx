import React, { useState } from 'react';
import TransactionTable from '../components/TransactionTable/TransactionTable';
import AggregatedTable from '../components/AggregatedTable/AggregatedTable'; // Ensure the path is correct
import styles from '../styles/Home.module.css';

export default function Home() {
  const [view, setView] = useState('transactions');

  return (
    <div className={styles.container}>
      <div className={styles.buttonContainer}>
        <button className={styles.viewButton} onClick={() => setView('transactions')}>Row View</button>
        <button className={styles.viewButton} onClick={() => setView('aggregated')}>Aggregated View</button>
      </div>

      {view === 'transactions' ? <TransactionTable /> : <AggregatedTable />}
    </div>
  );
}
