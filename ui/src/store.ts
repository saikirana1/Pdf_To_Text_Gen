import { create } from "zustand";

interface CounterState {
  status: string;
  setStatus: (value: string) => void;
  file?: string;
  setFile?: (value: string) => void;
}




export const useCounterStore = create<CounterState>((set) => ({
  status: "",
  file: "",
  setFile: (value: string) => set({ file: value }),
  setStatus: (value: string) => set({ status: value }),
}));


