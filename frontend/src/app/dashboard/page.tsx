"use client";

import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

type Equipment = {
  id: number;
  name: string;
  equipment_type: string;
  daily_rate: number;
  available: boolean;
};

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

export default function Dashboard() {
  const [equipment, setEquipment] = useState<Equipment[]>([]);
  const [rentals, setRentals] = useState<Rental[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboardData = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setError("You are not logged in.");
        return;
      }

      try {
        const [equipmentResponse, rentalsResponse] = await Promise.all([
          fetch("http://127.0.0.1:8000/equipment", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }),

          fetch("http://127.0.0.1:8000/rentals", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }),
        ]);

        if (!equipmentResponse.ok || !rentalsResponse.ok) {
          setError("Failed to load dashboard data.");
          return;
        }

        const equipmentData = await equipmentResponse.json();
        const rentalsData = await rentalsResponse.json();

        setEquipment(equipmentData);
        setRentals(rentalsData);
      } catch (error) {
        console.error(error);
        setError("Could not connect to the server.");
      }
    };

    fetchDashboardData();
  }, []);

  const availableEquipment = equipment.filter(
    (item) => item.available
  ).length;

  const rentedEquipment = equipment.filter(
    (item) => !item.available
  ).length;

  return (
    <div className="min-h-screen bg-slate-100 flex">

      <Sidebar />

      <main className="flex-1 min-w-0">

        <header className="bg-white border-b border-slate-200 px-8 py-5">
          <div className="max-w-7xl mx-auto flex items-center justify-between">

            <div>
              <h1 className="text-2xl font-bold text-slate-900">
                Equipment Rental ERP
              </h1>

              <p className="text-sm text-slate-500">
                Management Dashboard
              </p>
            </div>

          </div>
        </header>

        <div className="max-w-7xl mx-auto px-8 py-8">

          <h2 className="text-2xl font-semibold text-slate-900 mb-6">
            Dashboard
          </h2>

          {error && (
            <div className="mb-6 rounded-lg bg-red-100 p-4 text-red-700">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

            <div className="bg-white rounded-xl shadow-sm p-6">
              <p className="text-sm text-slate-500">
                Total Equipment
              </p>

              <p className="text-3xl font-bold text-slate-900 mt-2">
                {equipment.length}
              </p>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <p className="text-sm text-slate-500">
                Available Equipment
              </p>

              <p className="text-3xl font-bold text-green-600 mt-2">
                {availableEquipment}
              </p>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <p className="text-sm text-slate-500">
                Rented Equipment
              </p>

              <p className="text-3xl font-bold text-orange-600 mt-2">
                {rentedEquipment}
              </p>
            </div>

          </div>

          <div className="mt-8 bg-white rounded-xl shadow-sm p-6">

            <h3 className="text-lg font-semibold text-slate-900 mb-4">
              Equipment
            </h3>

            <div className="overflow-x-auto">

              <table className="w-full text-left">

                <thead>
                  <tr className="border-b border-slate-200">

                    <th className="py-3 text-sm text-slate-500">
                      ID
                    </th>

                    <th className="py-3 text-sm text-slate-500">
                      Equipment
                    </th>

                    <th className="py-3 text-sm text-slate-500">
                      Type
                    </th>

                    <th className="py-3 text-sm text-slate-500">
                      Daily Rate
                    </th>

                    <th className="py-3 text-sm text-slate-500">
                      Status
                    </th>

                  </tr>
                </thead>

                <tbody>

                  {equipment.map((item) => (
                    <tr
                      key={item.id}
                      className="border-b border-slate-100"
                    >

                      <td className="py-4">
                        {item.id}
                      </td>

                      <td className="py-4 font-medium">
                        {item.name}
                      </td>

                      <td className="py-4">
                        {item.equipment_type}
                      </td>

                      <td className="py-4">
                        ₹{item.daily_rate}
                      </td>

                      <td className="py-4">

                        {item.available ? (
                          <span className="text-green-600 font-medium">
                            Available
                          </span>
                        ) : (
                          <span className="text-orange-600 font-medium">
                            Rented
                          </span>
                        )}

                      </td>

                    </tr>
                  ))}

                </tbody>

              </table>

            </div>

          </div>

          <div className="mt-8 bg-white rounded-xl shadow-sm p-6">

            <h3 className="text-lg font-semibold text-slate-900 mb-4">
              Rentals
            </h3>

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

                  </tr>

                </thead>

                <tbody>

                  {rentals.map((rental) => (
                    <tr
                      key={rental.id}
                      className="border-b border-slate-100"
                    >

                      <td className="py-4">
                        {rental.id}
                      </td>

                      <td className="py-4">
                        {rental.customer_name}
                      </td>

                      <td className="py-4">
                        {rental.equipment_name}
                      </td>

                      <td className="py-4">
                        {rental.days}
                      </td>

                      <td className="py-4 font-medium">
                        ₹{rental.total_amount}
                      </td>

                    </tr>
                  ))}

                </tbody>

              </table>

            </div>

          </div>

        </div>

      </main>

    </div>
  );
}