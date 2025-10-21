import { create } from "zustand";

interface CounterState {
  status: string;
  files_urls: File[];
  check_box_urls?: ChooseFile[];
  setFileDetails: (value: File[]) => void;
  setStatus: (value: string) => void;
  file?: string;
  setFile?: (value: string) => void;
  setChooseFile?: (value: ChooseFile[]) => void;
  removeFileDetails: (fileName: string) => void;
  chatData: Message[];
   setChatData: (updater: Message[] | ((prev: Message[]) => Message[])) => void;
 
}
interface Message {
  role: "user" | "assistant";
  text: string;
}
export interface File {
  id?: any;
  file_name: string;
  file_url: string;
}
export interface ChooseFile{
  id?: any;
  file_name: string;
  file_url: string;
}

export const useCounterStore = create<CounterState>((set) => ({
  status: "",
  file: "",
  files_urls: [],
  check_box_urls: [],
  chatData: [],
  setFile: (value: string) => set({ file: value }),
  setStatus: (value: string) => set({ status: value }),
  setFileDetails: (value: File[]) =>
    set((state) => {
      const combinedFiles = [...state.files_urls, ...value];
      const uniqueFiles = combinedFiles.filter(
        (file, index, self) =>
          index === self.findIndex((f) => f.file_name === file.file_name)
      );
      return { files_urls: uniqueFiles };
    }),
  
  removeFileDetails: (fileName: string) =>
    set((state) => ({
      files_urls: state.files_urls.filter(
        (file) => file.file_name !== fileName
      ),
    })),
   setChooseFile: (value: ChooseFile[]) =>
    set({ check_box_urls: value }),
    setChatData: (updater) =>
    set((state) => ({
      chatData:
        typeof updater === "function" ? updater(state.chatData) : updater,
    })),
  // addMessage: (message: Message) =>
  //   set((state) => ({ chatData: [...state.chatData, message] })),
    
}));
