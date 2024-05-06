import axios from 'axios';

export const fetchData = async (url_with_queryParams, setData, callback_on_success, timestampField = "time_stamp", error_handler) => {
  try {
    const result = await axios.get(url_with_queryParams);
    console.info("result: ", result);
    setData(result.data);
    if (result.data && result.data.length > 0) {
      callback_on_success(result.data[result.data.length - 1][timestampField]);
    }
  } catch (error) {
    console.error('Error fetching data:', error);
    error_handler(error);
  }
};
