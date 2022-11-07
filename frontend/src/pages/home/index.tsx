import React from "react";
import Loader from "../../components/Loader";
import { useGetDevices } from "../../hooks/useGetDevices";
import { Places } from "./places";

interface IHomeProps {
  children?: JSX.Element | JSX.Element[];
}

const Home: React.FC<IHomeProps> = (props: IHomeProps) => {
  const {data, loading} = useGetDevices();
  if (loading) {
    return <Loader />;
  }

  return (
    <div className="grid content-baseline bg-background h-screen text-onBackground">
      <Places />
    </div>
  );
};

export { Home };
