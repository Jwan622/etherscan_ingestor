import 'dotenv/config';
import { pool } from "../../utils/db_pool"

const transaction_request_handler = async (req, res) => {
  const { timestamp, address, limit = 500 } = req.query;
  const queryParams = [];
  let query = `SELECT t.id, t.time_stamp, t.value, t.gas, t.gas_used,
              fa.address AS "from",
              ta.address AS "to"
              FROM transactions t
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

  query += ' ORDER BY t.time_stamp ASC LIMIT $' + (queryParams.length + 1);
  queryParams.push(limit);

  console.log("query: ", query);
  console.log("queryParams: ", queryParams);

  try {
    const { rows } = await pool.query(query, queryParams);
    console.log("some rows retrieved: ", rows.slice(0, 10));
    res.status(200).json(rows);
  } catch (error) {
    console.error("API Error:", error);
    res.status(500).json({ error: error.message });
  }
};

export default transaction_request_handler;
