import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TransactionTable from '../../../components/TransactionTable/TransactionTable';
import { act } from 'react-dom/test-utils';
import { fetchData } from "../../../utils/apiUtils";

jest.mock('../../../utils/apiUtils', () => ({
  fetchData: jest.fn()
}));



describe('TransactionTable', () => {
  beforeEach(() => {
    fetchData.mockImplementation((url, setTransactions, setLastTimestamp, errorHandling) => {
      setTransactions(
        [
          { id: '1', from: 'Alice1', to: 'Bob1', value: '101', gas: '500', gas_used: '300', time_stamp: '2021-05-04T21:20:00Z' },
          { id: '2', from: 'Alice2', to: 'Bob2', value: '102', gas: '500', gas_used: '300', time_stamp: '2021-05-04T22:20:00Z' },
          { id: '3', from: 'Alice3', to: 'Bob3', value: '103', gas: '500', gas_used: '300', time_stamp: '2021-05-04T23:20:00Z' },
          { id: '4', from: 'Alice4', to: 'Bob4', value: '104', gas: '500', gas_used: '300', time_stamp: '2021-05-04T24:20:00Z' },
          { id: '5', from: 'Alice5', to: 'Bob5', value: '105', gas: '500', gas_used: '300', time_stamp: '2021-05-04T25:20:00Z' },
          { id: '6', from: 'Alice6', to: 'Bob6', value: '106', gas: '500', gas_used: '300', time_stamp: '2021-05-04T26:20:00Z' }
        ]
      );
      setLastTimestamp('2021-05-04T20:20:01Z');
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('displays the default heading "Row by Row Table Involving ALL ADDRESSES"', async () => {
    await act(async () => {
      render(<TransactionTable />);
    });


    expect(screen.getByText("Row by Row Table Involving ALL ADDRESSES")).toBeInTheDocument();
  });

  it('has exactly 6 headers in the table', async () => {
    await act(async () => {
      render(<TransactionTable />);
    });

    const headers = screen.getAllByRole('columnheader');

    expect(headers).toHaveLength(6);
    expect(headers[0]).toHaveTextContent('From');
    expect(headers[1]).toHaveTextContent('To');
    expect(headers[2]).toHaveTextContent('Value');
    expect(headers[3]).toHaveTextContent('Gas');
    expect(headers[4]).toHaveTextContent('Gas Used');
    expect(headers[5]).toHaveTextContent('Timestamp');
  });

  it("updates the heading with the searched for address", async () => {
    await act(async () => {
      render(<TransactionTable />);
    });

    // Check initial state
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Row by Row Table Involving ALL ADDRESSES');

    const addressInput = screen.getByPlaceholderText('Search by address');
    const timestampInput = screen.getByPlaceholderText('Search by date (YYYY-MM-DD HH:MM:SS)');
    const submitButton = screen.getByRole('button', { name: /search/i });

    fireEvent.change(addressInput, { target: { value: '0x123456789' } });
    fireEvent.change(timestampInput, { target: { value: '2021-05-04T20:20:00Z' } });
    fireEvent.click(submitButton);

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Row by Row Table Involving Account: 0x123456789');
  })

  it('it renders the search button and it is initially disabled', async () => {
    await act(async () => {
      render(<TransactionTable />);
    });

    const searchButton = screen.getByRole('button', { name: /search/i });

    expect(searchButton).toBeInTheDocument();

    expect(searchButton).toBeDisabled();
  });

  it('button becomes enabled when input conditions are met', async () => {
    await act(async () => {
      render(<TransactionTable />);
    });

    const addressInput = screen.getByPlaceholderText('Search by address');
    const timestampInput = screen.getByPlaceholderText('Search by date (YYYY-MM-DD HH:MM:SS)');

    fireEvent.change(addressInput, { target: { value: '0x123...' } });
    fireEvent.change(timestampInput, { target: { value: '2021-01-01 00:00:00' } });

    const searchButton = screen.getByRole('button', { name: /search/i });

    expect(searchButton).not.toBeDisabled();
  });
});
