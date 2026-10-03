"use client";

import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

type Rental = {
  id: number;
  customer_id: number;
  customer_name: string;
  equipment_id: number;
  equipment_name: string;
  days: number;
  total_amount: number;
  returned: boolean;
};

type Customer = {
  id: number;
  name: string;
  phone: string;
  email: string;
};

type Equipment = {
  id: number;
  name: string;
  equipment_type: string;
  daily_rate: number;
  available: boolean;
};

export default function RentalsPage() {
  const [rentals, setRentals] = useState<Rental[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [equipment, setEquipment] = useState<Equipment[]>([]);

  const [selectedCustomer, setSelectedCustomer] = useState("");
  const [selectedEquipment, setSelectedEquipment] = useState("");
  const [days, setDays] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [returningId, setReturningId] = useState<number | null>(null);
  const [creatingRental, setCreatingRental] = useState(false);

  const fetchRentals = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("You are not logged in.");
      return;
    }

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/rentals`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to load rentals.");
        return;
      }

      setRentals(data);
    } catch (error) {
      console.error(error);
      setError("Could not connect to the server.");
    }
  };

  const fetchFormData = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("You are not logged in.");
      return;
    }

    try {
      const [customersResponse, equipmentResponse] =
        await Promise.all([
          fetch(`${process.env.NEXT_PUBLIC_API_URL}/customers`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }),

          fetch(`${process.env.NEXT_PUBLIC_API_URL}/equipment`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }),
        ]);

      const customersData = await customersResponse.json();
      const equipmentData = await equipmentResponse.json();

      if (!customersResponse.ok) {
        setError(
          customersData.detail || "Failed to load customers."
        );
        return;
      }

      if (!equipmentResponse.ok) {
        setError(
          equipmentData.detail || "Failed to load equipment."
        );
        return;
      }

      setCustomers(customersData);
      setEquipment(equipmentData);
    } catch (error) {
      console.error(error);
      setError("Could not load rental form data.");
    }
  };

  useEffect(() => {
    fetchRentals();
    fetchFormData();
  }, []);

  const handleCreateRental = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("You are not logged in.");
      return;
    }

    if (!selectedCustomer || !selectedEquipment || !days) {
      setError("Please fill in all rental fields.");
      return;
    }

    const rentalDays = Number(days);

    if (rentalDays <= 0) {
      setError("Rental days must be greater than 0.");
      return;
    }

    setCreatingRental(true);
    setError("");
    setSuccess("");

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/rentals`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            customer_id: Number(selectedCustomer),
            equipment_id: Number(selectedEquipment),
            days: rentalDays,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to create rental.");
        return;
      }

      setSuccess(
        `Rental #${data.id} created successfully.`
      );

      setSelectedCustomer("");
      setSelectedEquipment("");
      setDays("");

      await fetchRentals();
      await fetchFormData();

    } catch (error) {
      console.error(error);
      setError("Could not connect to the server.");
    } finally {
      setCreatingRental(false);
    }
  };

  const handleReturn = async (rentalId: number) => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("You are not logged in.");
      return;
    }

    setReturningId(rentalId);
    setError("");
    setSuccess("");

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/rentals/${rentalId}/return`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(
          data.detail || "Failed to return equipment."
        );
        return;
      }

      setSuccess("Equipment returned successfully.");

      await fetchRentals();
      await fetchFormData();

    } catch (error) {
      console.error(error);
      setError("Could not connect to the server.");
    } finally {
      setReturningId(null);
    }
  };

  const activeRentals = rentals.filter(
    (rental) => !rental.returned
  ).length;

  const completedRentals = rentals.filter(
    (rental) => rental.returned
  ).length;

  const availableEquipment = equipment.filter(
    (item) => item.available
  );

  return (
    <div className="min-h-screen bg-slate-100 flex">

      <Sidebar />

      <main className="flex-1 min-w-0">

        <header className="bg-white border-b border-slate-200 px-8 py-5">
          <div className="max-w-7xl mx-auto">

            <h1 className="text-2xl font-bold text-slate-900">
              Rentals
            </h1>

            <p className="text-sm text-slate-500 mt-1">
              Manage equipment rental transactions
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

          {/* Rental Summary */}

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">

            <div className="bg-white rounded-xl shadow-sm p-6">

              <p className="text-sm text-slate-500">
                Total Rentals
              </p>

              <p className="text-3xl font-bold text-slate-900 mt-2">
                {rentals.length}
              </p>

            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">

              <p className="text-sm text-slate-500">
                Active Rentals
              </p>

              <p className="text-3xl font-bold text-orange-600 mt-2">
                {activeRentals}
              </p>

            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">

              <p className="text-sm text-slate-500">
                Completed Rentals
              </p>

              <p className="text-3xl font-bold text-green-600 mt-2">
                {completedRentals}
              </p>

            </div>

          </div>

          {/* Create Rental */}

          <div className="bg-white rounded-xl shadow-sm p-6 mb-8">

            <div className="mb-6">

              <h2 className="text-lg font-semibold text-slate-900">
                Create Rental
              </h2>

              <p className="text-sm text-slate-500 mt-1">
                Create a new equipment rental transaction
              </p>

            </div>

            <form
              onSubmit={handleCreateRental}
              className="grid grid-cols-1 md:grid-cols-3 gap-6"
            >

              <div>

                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Customer
                </label>

                <select
                  value={selectedCustomer}
                  onChange={(event) =>
                    setSelectedCustomer(event.target.value)
                  }
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 text-slate-900 focus:border-slate-500 focus:outline-none"
                >

                  <option value="">
                    Select customer
                  </option>

                  {customers.map((customer) => (
                    <option
                      key={customer.id}
                      value={customer.id}
                    >
                      {customer.name}
                    </option>
                  ))}

                </select>

              </div>

              <div>

                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Equipment
                </label>

                <select
                  value={selectedEquipment}
                  onChange={(event) =>
                    setSelectedEquipment(event.target.value)
                  }
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 text-slate-900 focus:border-slate-500 focus:outline-none"
                >

                  <option value="">
                    Select available equipment
                  </option>

                  {availableEquipment.map((item) => (
                    <option
                      key={item.id}
                      value={item.id}
                    >
                      {item.name} — ₹{item.daily_rate}/day
                    </option>
                  ))}

                </select>

              </div>

              <div>

                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Rental Days
                </label>

                <input
                  type="number"
                  min="1"
                  value={days}
                  onChange={(event) =>
                    setDays(event.target.value)
                  }
                  placeholder="Enter number of days"
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 text-slate-900 focus:border-slate-500 focus:outline-none"
                />

              </div>

              <div className="md:col-span-3">

                <button
                  type="submit"
                  disabled={creatingRental}
                  className="rounded-lg bg-slate-900 px-6 py-3 text-sm font-medium text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {creatingRental
                    ? "Creating Rental..."
                    : "Create Rental"}
                </button>

              </div>

            </form>

          </div>

          {/* Rental Transactions */}

          <div className="bg-white rounded-xl shadow-sm p-6">

            <div className="mb-6">

              <h2 className="text-lg font-semibold text-slate-900">
                Rental Transactions
              </h2>

              <p className="text-sm text-slate-500 mt-1">
                View and manage rental history
              </p>

            </div>

            <div className="overflow-x-auto">

              <table className="w-full text-left">

                <thead>

                  <tr className="border-b border-slate-200">

                    <th className="py-3 text-sm text-slate-500">
                      Rental ID
                    </th>

                    <th className="py-3 text-sm text-slate-500">
                      Customer
                    </th>

                    <th className="py-3 text-sm text-slate-500">
                      Equipment
                    </th>

                    <th className="py-3 text-sm text-slate-500">
                      Days
                    </th>

                    <th className="py-3 text-sm text-slate-500">
                      Total
                    </th>

                    <th className="py-3 text-sm text-slate-500">
                      Status
                    </th>

                    <th className="py-3 text-sm text-slate-500">
                      Action
                    </th>

                  </tr>

                </thead>

                <tbody>

                  {rentals.map((rental) => (
                    <tr
                      key={rental.id}
                      className="border-b border-slate-100"
                    >

                      <td className="py-4 text-slate-700">
                        {rental.id}
                      </td>

                      <td className="py-4 font-medium text-slate-900">
                        {rental.customer_name}
                      </td>

                      <td className="py-4 text-slate-700">
                        {rental.equipment_name}
                      </td>

                      <td className="py-4 text-slate-700">
                        {rental.days}
                      </td>

                      <td className="py-4 font-medium text-slate-900">
                        ₹{rental.total_amount}
                      </td>

                      <td className="py-4">

                        {rental.returned ? (
                          <span className="inline-flex rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-700">
                            Returned
                          </span>
                        ) : (
                          <span className="inline-flex rounded-full bg-orange-100 px-3 py-1 text-sm font-medium text-orange-700">
                            Active
                          </span>
                        )}

                      </td>

                      <td className="py-4">

                        {!rental.returned && (
                          <button
                            onClick={() =>
                              handleReturn(rental.id)
                            }
                            disabled={
                              returningId === rental.id
                            }
                            className="rounded-lg bg-slate-900 px-3 py-2 text-sm font-medium text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
                          >
                            {returningId === rental.id
                              ? "Returning..."
                              : "Return"}
                          </button>
                        )}

                        {rental.returned && (
                          <span className="text-sm text-slate-400">
                            Completed
                          </span>
                        )}

                      </td>

                    </tr>
                  ))}

                </tbody>

              </table>

              {rentals.length === 0 && !error && (
                <div className="py-10 text-center text-slate-500">
                  No rentals found.
                </div>
              )}

            </div>

          </div>

        </div>

      </main>

    </div>
  );
}
