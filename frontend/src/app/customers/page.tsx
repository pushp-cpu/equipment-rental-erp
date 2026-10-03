"use client";

import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

type Customer = {
  id: number;
  name: string;
  phone: string;
  email: string;
};

export default function CustomersPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);

  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [creating, setCreating] = useState(false);

  const fetchCustomers = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("You are not logged in.");
      return;
    }

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/customers",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to load customers.");
        return;
      }

      setCustomers(data);
    } catch (error) {
      console.error(error);
      setError("Could not connect to the server.");
    }
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const handleCreateCustomer = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("You are not logged in.");
      return;
    }

    if (!name || !phone || !email) {
      setError("Please fill in all customer fields.");
      return;
    }

    setCreating(true);
    setError("");
    setSuccess("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/customers",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            name,
            phone,
            email,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to create customer.");
        return;
      }

      setSuccess(
        `Customer #${data.id} created successfully.`
      );

      setName("");
      setPhone("");
      setEmail("");

      await fetchCustomers();

    } catch (error) {
      console.error(error);
      setError("Could not connect to the server.");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex">

      <Sidebar />

      <main className="flex-1 min-w-0">

        <header className="bg-white border-b border-slate-200 px-8 py-5">
          <div className="max-w-7xl mx-auto">

            <h1 className="text-2xl font-bold text-slate-900">
              Customers
            </h1>

            <p className="text-sm text-slate-600 mt-1">
              Manage rental customers
            </p>

          </div>
        </header>

        <div className="max-w-7xl mx-auto px-8 py-8">

          {error && (
            <div className="mb-6 rounded-lg bg-red-100 p-4 text-red-700">
              {error}
            </div>
          )}

          {success && (
            <div className="mb-6 rounded-lg bg-green-100 p-4 text-green-700">
              {success}
            </div>
          )}

          {/* Create Customer */}

          <div className="bg-white rounded-xl shadow-sm p-6 mb-8">

            <div className="mb-6">

              <h2 className="text-lg font-semibold text-slate-900">
                Add Customer
              </h2>

              <p className="text-sm text-slate-600 mt-1">
                Add a new customer to the system
              </p>

            </div>

            <form
              onSubmit={handleCreateCustomer}
              className="grid grid-cols-1 md:grid-cols-2 gap-6"
            >

              <div>

                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Name
                </label>

                <input
                  type="text"
                  value={name}
                  onChange={(event) =>
                    setName(event.target.value)
                  }
                  placeholder="Enter customer name"
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 text-slate-900 focus:border-slate-500 focus:outline-none"
                />

              </div>

              <div>

                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Phone
                </label>

                <input
                  type="text"
                  value={phone}
                  onChange={(event) =>
                    setPhone(event.target.value)
                  }
                  placeholder="Enter phone number"
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 text-slate-900 focus:border-slate-500 focus:outline-none"
                />

              </div>

              <div>

                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Email
                </label>

                <input
                  type="email"
                  value={email}
                  onChange={(event) =>
                    setEmail(event.target.value)
                  }
                  placeholder="Enter email address"
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 text-slate-900 focus:border-slate-500 focus:outline-none"
                />

              </div>

              <div className="flex items-end">

                <button
                  type="submit"
                  disabled={creating}
                  className="rounded-lg bg-slate-900 px-6 py-3 text-sm font-medium text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {creating
                    ? "Adding Customer..."
                    : "Add Customer"}
                </button>

              </div>

            </form>

          </div>

          {/* Customer List */}

          <div className="bg-white rounded-xl shadow-sm p-6">

            <div className="mb-6">

              <h2 className="text-lg font-semibold text-slate-900">
                Customer Directory
              </h2>

              <p className="text-sm text-slate-600 mt-1">
                {customers.length} customers
              </p>

            </div>

            <div className="overflow-x-auto">

              <table className="w-full text-left">

                <thead>

                  <tr className="border-b border-slate-200">

                    <th className="py-3 text-sm font-semibold text-slate-600">
                      ID
                    </th>

                    <th className="py-3 text-sm font-semibold text-slate-600">
                      Name
                    </th>

                    <th className="py-3 text-sm font-semibold text-slate-600">
                      Phone
                    </th>

                    <th className="py-3 text-sm font-semibold text-slate-600">
                      Email
                    </th>

                  </tr>

                </thead>

                <tbody>

                  {customers.map((customer) => (
                    <tr
                      key={customer.id}
                      className="border-b border-slate-100"
                    >

                      <td className="py-4 text-slate-900">
                        {customer.id}
                      </td>

                      <td className="py-4 font-medium text-slate-900">
                        {customer.name}
                      </td>

                      <td className="py-4 text-slate-900">
                        {customer.phone}
                      </td>

                      <td className="py-4 text-slate-900">
                        {customer.email}
                      </td>

                    </tr>
                  ))}

                </tbody>

              </table>

              {customers.length === 0 && !error && (
                <div className="py-10 text-center text-slate-600">
                  No customers found.
                </div>
              )}

            </div>

          </div>

        </div>

      </main>

    </div>
  );
}