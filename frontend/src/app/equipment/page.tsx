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

export default function EquipmentPage() {
  const [equipment, setEquipment] = useState<Equipment[]>([]);

  const [name, setName] = useState("");
  const [equipmentType, setEquipmentType] = useState("");
  const [dailyRate, setDailyRate] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [creating, setCreating] = useState(false);

  const fetchEquipment = async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("You are not logged in.");
      return;
    }

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/equipment`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to load equipment.");
        return;
      }

      setEquipment(data);
    } catch (error) {
      console.error(error);
      setError("Could not connect to the server.");
    }
  };

  useEffect(() => {
    fetchEquipment();
  }, []);

  const handleCreateEquipment = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("You are not logged in.");
      return;
    }

    if (!name || !equipmentType || !dailyRate) {
      setError("Please fill in all equipment fields.");
      return;
    }

    const rate = Number(dailyRate);

    if (rate <= 0) {
      setError("Daily rate must be greater than 0.");
      return;
    }

    setCreating(true);
    setError("");
    setSuccess("");

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/equipment`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            name,
            equipment_type: equipmentType,
            daily_rate: rate,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to create equipment.");
        return;
      }

      setSuccess(
        `Equipment #${data.id} created successfully.`
      );

      setName("");
      setEquipmentType("");
      setDailyRate("");

      await fetchEquipment();

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
              Equipment
            </h1>

            <p className="text-sm text-slate-600 mt-1">
              Manage rental equipment and availability
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

          {/* Add Equipment */}

          <div className="bg-white rounded-xl shadow-sm p-6 mb-8">

            <div className="mb-6">

              <h2 className="text-lg font-semibold text-slate-900">
                Add Equipment
              </h2>

              <p className="text-sm text-slate-600 mt-1">
                Add new equipment to the rental inventory
              </p>

            </div>

            <form
              onSubmit={handleCreateEquipment}
              className="grid grid-cols-1 md:grid-cols-3 gap-6"
            >

              <div>

                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Equipment Name
                </label>

                <input
                  type="text"
                  value={name}
                  onChange={(event) =>
                    setName(event.target.value)
                  }
                  placeholder="e.g. CAT Excavator"
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 text-slate-900 focus:border-slate-500 focus:outline-none"
                />

              </div>

              <div>

                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Equipment Type
                </label>

                <input
                  type="text"
                  value={equipmentType}
                  onChange={(event) =>
                    setEquipmentType(event.target.value)
                  }
                  placeholder="e.g. Excavator"
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 text-slate-900 focus:border-slate-500 focus:outline-none"
                />

              </div>

              <div>

                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Daily Rental Rate
                </label>

                <input
                  type="number"
                  min="1"
                  value={dailyRate}
                  onChange={(event) =>
                    setDailyRate(event.target.value)
                  }
                  placeholder="e.g. 8000"
                  className="w-full rounded-lg border border-slate-300 px-4 py-3 text-slate-900 focus:border-slate-500 focus:outline-none"
                />

              </div>

              <div className="md:col-span-3">

                <button
                  type="submit"
                  disabled={creating}
                  className="rounded-lg bg-slate-900 px-6 py-3 text-sm font-medium text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {creating
                    ? "Adding Equipment..."
                    : "Add Equipment"}
                </button>

              </div>

            </form>

          </div>

          {/* Equipment Inventory */}

          <div className="bg-white rounded-xl shadow-sm p-6">

            <div className="mb-6">

              <h2 className="text-lg font-semibold text-slate-900">
                Equipment Inventory
              </h2>

              <p className="text-sm text-slate-600 mt-1">
                {equipment.length} equipment items
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
                      Equipment
                    </th>

                    <th className="py-3 text-sm font-semibold text-slate-600">
                      Type
                    </th>

                    <th className="py-3 text-sm font-semibold text-slate-600">
                      Daily Rate
                    </th>

                    <th className="py-3 text-sm font-semibold text-slate-600">
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

                      <td className="py-4 text-slate-900">
                        {item.id}
                      </td>

                      <td className="py-4 font-medium text-slate-900">
                        {item.name}
                      </td>

                      <td className="py-4 text-slate-900">
                        {item.equipment_type}
                      </td>

                      <td className="py-4 text-slate-900">
                        ₹{item.daily_rate}
                      </td>

                      <td className="py-4">

                        {item.available ? (
                          <span className="inline-flex rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-700">
                            Available
                          </span>
                        ) : (
                          <span className="inline-flex rounded-full bg-orange-100 px-3 py-1 text-sm font-medium text-orange-700">
                            Rented
                          </span>
                        )}

                      </td>

                    </tr>
                  ))}

                </tbody>

              </table>

              {equipment.length === 0 && !error && (
                <div className="py-10 text-center text-slate-600">
                  No equipment found.
                </div>
              )}

            </div>

          </div>

        </div>

      </main>

    </div>
  );
}
