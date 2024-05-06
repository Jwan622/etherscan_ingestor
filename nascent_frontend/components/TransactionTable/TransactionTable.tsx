import React, { useState, useEffect } from 'react';
import DualFieldSearchBar from '../DualFieldSearchBar/DualFieldSearchBar';
import { fetchData } from '../../utils/apiUtils';
import styles from './TransactionTable.module.css';
import tableStyles from '../../styles/shared/table.module.css';

const TransactionTable = () => {
  const [transactions, setTransactions] = useState([]);
  const initialTimestamp = '2021-05-04T20:20:00Z';
  const [lastTimestamp, setLastTimestamp] = useState(initialTimestamp);

  useEffect(() => {
    const url = `/api/transactions?limit=500&timestamp=${encodeURIComponent(lastTimestamp)}`;
    fetchData(url, setTransactions, (newLastTimestamp) => setLastTimestamp(newLastTimestamp), "time_stamp", console.error);
  }, []);

  const handleSearch = (timestamp, address=null) => {
    const timestampParam = timestamp ? `&timestamp=${encodeURIComponent(timestamp)}` : '';
    const addressParam = address ? `&address=${encodeURIComponent(address)}` : '';
    const url = `/api/transactions?limit=500${timestampParam}${addressParam}`;
    const newLastTimeStampIncrement = (newLastTimestamp) => {
      const date = new Date(newLastTimestamp);
      date.setMilliseconds(date.getMilliseconds() + 1);
      setLastTimestamp(date.toISOString());
    }

    fetchData(url, setTransactions, newLastTimeStampIncrement, "time_stamp", console.error);
  };

  return (
    <>
      <h1>Row by Row Table Involving Account: </h1>
      <div className={styles.searchContainer}>
        <DualFieldSearchBar onSubmit={(params) => handleSearch(params.timestamp, params.address)}/>
      </div>
      <div className={styles.buttonGroup}>
        <button className={styles.resetButton} onClick={() => handleSearch(initialTimestamp)}>Reset</button>
        <button className={styles.loadMoreButton} onClick={() => handleSearch(lastTimestamp)}>Load More</button>
      </div>
      <div className={tableStyles.tableContainer}>
        <table>
          <thead className={tableStyles.tableHeader}>
          <tr className={tableStyles.tr}>
            <th className={tableStyles.th}>From</th>
            <th className={tableStyles.th}>To</th>
            <th className={tableStyles.th}>Value</th>
            <th className={tableStyles.th}>Gas</th>
            <th className={tableStyles.th}>Gas Used</th>
            <th className={tableStyles.th}>Timestamp</th>
          </tr>
          </thead>
          <tbody>
          {transactions.map(tx => (
            <tr key={tx.id} className={tableStyles.tr}>
              <td className={tableStyles.td}>{tx.from}</td>
              <td className={tableStyles.td}>{tx.to}</td>
              <td className={tableStyles.td}>{tx.value}</td>
              <td className={tableStyles.td}>{tx.gas}</td>
              <td className={tableStyles.td}>{tx.gas_used}</td>
              <td className={tableStyles.td}>{tx.time_stamp}</td>
            </tr>
          ))}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default TransactionTable;
