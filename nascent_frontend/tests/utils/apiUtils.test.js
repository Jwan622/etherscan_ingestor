import axios from 'axios';
import { fetchData } from '../../utils/apiUtils'; // Adjust the path to where fetchData is exported

jest.mock('axios');

describe('fetchData', () => {
  const mockSetData = jest.fn();
  const mockCallbackOnSuccess = jest.fn();
  const mockErrorHandler = jest.fn();
  const url = 'http://etherscan.com';

  beforeEach(() => {
    jest.resetAllMocks(); // Reset all mocks fresh for each test
    axios.get.mockResolvedValue({ data: [] }); // Default to empty data
  });

  test('fetches data successfully and calls setData and callback_on_success with the last time_stamp field', async () => {
    const mockData = {
      data: [{ id: 1, time_stamp: '2022-05-01T00:00:00Z' }, { id: 2, time_stamp: '2022-05-02T00:00:00Z' }]
    };
    axios.get.mockResolvedValue(mockData);

    await fetchData(url, mockSetData, mockCallbackOnSuccess);

    expect(axios.get).toHaveBeenCalledWith(url);
    expect(mockSetData).toHaveBeenCalledWith(mockData.data);
    expect(mockCallbackOnSuccess).toHaveBeenCalledWith('2022-05-02T00:00:00Z');
  });

  test('fetches data successfully and calls setData and callback_on_success with the last date field', async () => {
    const mockData = {
      data: [{ id: 1, date: '2022-05-01' }, { id: 2, date: '2022-05-02' }]
    };
    axios.get.mockResolvedValue(mockData);

    await fetchData(url, mockSetData, mockCallbackOnSuccess, "date");

    expect(axios.get).toHaveBeenCalledWith(url);
    expect(mockSetData).toHaveBeenCalledWith(mockData.data);
    expect(mockCallbackOnSuccess).toHaveBeenCalledWith('2022-05-02');
  });

  test('successful data fetch', async () => {
    const mockData = { data: [{ id: 1, time_stamp: '2022-05-01T00:00:00Z' }] };
    axios.get.mockResolvedValue(mockData);

    await fetchData(url, mockSetData, mockCallbackOnSuccess, 'time_stamp', mockErrorHandler);

    expect(axios.get).toHaveBeenCalledWith(url);
    expect(mockSetData).toHaveBeenCalledWith(mockData.data);
    expect(mockCallbackOnSuccess).toHaveBeenCalledWith('2022-05-01T00:00:00Z');
  });

  test('network error handling', async () => {
    const error = new Error('Network error');
    axios.get.mockRejectedValue(error);

    await fetchData(url, mockSetData, mockCallbackOnSuccess, 'time_stamp', mockErrorHandler);

    expect(axios.get).toHaveBeenCalledWith(url);
    expect(mockErrorHandler).toHaveBeenCalledWith(error);
  });
});
