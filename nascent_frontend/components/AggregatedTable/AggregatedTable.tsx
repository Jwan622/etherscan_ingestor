import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { parseISO, format } from 'date-fns';
import DualFieldSearchBar from '../DualFieldSearchBar/DualFieldSearchBar';
import styles from '../TransactionTable/TransactionTable.module.css';
import tableStyles from '../../styles/shared/table.module.css'
import { fetchData } from '../../utils/apiUtils';

const AggregatedTable = () => {
  const [aggregatedData, setAggregatedData] = useState([]);
  const initialDay = '2021-05-04';
  const [lastDay, setLastDay] = useState(initialDay);


  useEffect(() => {
    fetchData('/api/aggregated', setAggregatedData, (newLastDay) => setLastDay(newLastDay), "day", console.error);
  }, []);

  const handleAggregatedSearch = ({ timestamp, address=null }) => {
    const timestampParam = timestamp ? `&timestamp=${encodeURIComponent(timestamp)}` : '';
    const addressParam = address ? `&address=${encodeURIComponent(address)}` : '';
    const url = `/api/aggregated?limit=50${timestampParam}${addressParam}`;
    const newLastDayIncrement = (newLastDay) => {
      const date = new Date(newLastDay);
      date.setDate(date.getDate() + 1);
      setLastDay(date.toISOString());
    }
    fetchData(url, setAggregatedData, newLastDayIncrement, "day", console.error);
  }

  return (
    <>
      <h1>Aggregations involving account:</h1>
      <div className={styles.searchContainer}>
        <DualFieldSearchBar onSubmit={(params) => handleAggregatedSearch({timestamp: params.timestamp, address: params.address})}/>
      </div>
      <div className={styles.buttonGroup}>
        <button className={styles.resetButton} onClick={() => handleAggregatedSearch({timestamp: initialDay})}>Reset</button>
        <button className={styles.loadMoreButton} onClick={() => handleAggregatedSearch({timestamp: lastDay})}>Load More</button>
      </div>
      <div className={tableStyles.tableContainer}>
        <table>
          <thead className={tableStyles.tableHeader}>
          <tr className={tableStyles.tr}>
            <th className={tableStyles.th}>Day</th>
            <th className={tableStyles.th}>Count</th>
          </tr>
          </thead>
          <tbody>
          {aggregatedData.map((data, index) => (
            <tr key={index} className={tableStyles.tr}>
              <td className={tableStyles.td}>{format(parseISO(data.day), 'yyyy-MM-dd')}</td>
              <td className={tableStyles.td}>{data.transaction_count}</td>
            </tr>
          ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

export default AggregatedTable;
