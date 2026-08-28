import React, { useEffect, useState } from 'react';
import { Activity } from '../types';
import { fetchActivities } from '../services/api';
import ActivityCard from '../components/ActivityCard';

const Dashboard: React.FC = () => {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    const loadActivities = async () => {
      try {
        const response = await fetchActivities();
        setActivities(response.results || []);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    loadActivities();
    const interval = setInterval(loadActivities, 5000); // Refrescar cada 5s
    return () => clearInterval(interval);
  }, []);

  const filteredActivities = filter === 'all' 
    ? activities 
    : activities.filter(a => a.activity_type === filter);

  if (loading) return <div className="p-8 text-center">Cargando...</div>;
  if (error) return <div className="p-8 text-red-500">Error: {error}</div>;

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Dashboard de Actividades Sospechosas</h1>
      
      <div className="mb-4 flex gap-2">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded ${filter === 'all' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
        >
          Todas ({activities.length})
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredActivities.map(activity => (
          <ActivityCard
            key={activity.id}
            activity={activity}
            onViewDetails={(id) => console.log(`Ver: ${id}`)}
          />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
