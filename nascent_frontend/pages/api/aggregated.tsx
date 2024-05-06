import 'dotenv/config';
import { NextApiRequest, NextApiResponse } from 'next';
import { pool } from "../../utils/db_pool"

const aggregate_transactions_handler = async (req: NextApiRequest, res: NextApiResponse) => {
  const { timestamp, address, limit = 50 } = req.query;
  const queryParams = [];

  let query = `
    SELECT
        DATE(time_stamp) AS day,
        COUNT(*) AS transaction_count
    FROM transactions AS t
    INNER JOIN addresses fa ON t.from_address_id = fa.id
    INNER JOIN addresses ta ON t.to_address_id = ta.id`;

  if (timestamp) {
    query += ' WHERE t.time_stamp > $1';
    queryParams.push(timestamp);
  }
  if (address) {
    if (timestamp) {
      query += ' AND';
    } else {
      query += ' WHERE';
    }
    query += ' (fa.address = $' + (queryParams.length + 1) + ' OR ta.address = $' + (queryParams.length + 1) + ')';
    queryParams.push(address);
  }

  query += ` GROUP BY
      DATE(time_stamp)
  ORDER BY
      DATE(time_stamp)`

  query += ' LIMIT $' + (queryParams.length + 1) + ';';
  queryParams.push(limit);
  console.log('query: ', query)
  console.log('queryParams: ', queryParams)
  try {
    const { rows } = await pool.query(query, queryParams);
    res.status(200).json(rows);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

export default aggregate_transactions_handler;
