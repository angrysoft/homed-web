"use client";
import { useContext, useEffect } from "react";
import { AppContext } from "../store";

const useEvents = () => {
  const { dispatch } = useContext(AppContext);

  useEffect(() => {
    console.log("init event source");
    const evSource = new EventSource("http://localhost:8080/devices/events");
    evSource.onmessage = async (event) => {
      console.log(event);
      if (!event.data.startsWith("{")) return;
      const eventData = JSON.parse(event.data);
      switch (eventData.sid) {
        case "deviceManager": {
          dispatch({
            type: "REFRESH_NEEDED_TRUE",
            payload: eventData.payload.deviceList || [],
          });
          break;
        }
        default: {
          console.log(event.data);
          dispatch({ type: "UPDATE_DEVICE", payload: eventData });
          break;
        }
      }
    };
  }, [dispatch]);
};

export { useEvents };
