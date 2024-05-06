import React from 'react';
import { render, screen } from '@testing-library/react';
import TransactionTable from './TransactionTable';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

const mock = new MockAdapter(axios);
const mockData = Array.from({ length: 10 }, (_, index) => ({
  id: index,
  from: `address_from_${index}`,
  to: `address_to_${index}`,
  value: `value_${index}`,
  gas: `gas_${index}`,
  gas_used: `gas_used_${index}`,
  time_stamp: `2021-05-04T20:20:${index}Z`
}));

mock.onGet("/api/transactions").reply(200, mockData);

describe('TransactionTable', () => {
  test('displays the default heading "Row by Row Involving ALL ACCOUNTS"', () => {
    render(<TransactionTable />);
    expect(screen.getByText("Row by Row Involving ALL ACCOUNTS")).toBeInTheDocument();
  });

  test('has exactly 6 headers in the table', () => {
    render(<TransactionTable />);

    const headers = screen.getAllByRole('columnheader');

    expect(headers).toHaveLength(6);
    expect(headers[0]).toHaveTextContent('From');
    expect(headers[1]).toHaveTextContent('To');
    expect(headers[2]).toHaveTextContent('Value');
    expect(headers[3]).toHaveTextContent('Gas');
    expect(headers[4]).toHaveTextContent('Gas Used');
    expect(headers[5]).toHaveTextContent('Timestamp');
  });
});
