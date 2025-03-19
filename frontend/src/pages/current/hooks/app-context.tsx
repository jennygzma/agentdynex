import React, {
  Dispatch,
  SetStateAction,
  createContext,
  useContext,
  useState,
} from "react";

export interface TreeNode {
  [key: string]: TreeNode | undefined;
}

export interface AppState {
  isLoading: boolean;
  updateIsLoading: Dispatch<SetStateAction<Boolean>>;
  currentRunId: string;
  updateCurrentRunId: Dispatch<SetStateAction<string>>;
  isRunningSimulation: boolean;
  updateIsRunningSimulation: Dispatch<SetStateAction<boolean>>;
  currentRunTree: TreeNode;
  updateCurrentRunTree: Dispatch<SetStateAction<TreeNode>>;
  prototypes: string[];
  updatePrototypes: Dispatch<SetStateAction<string[]>>;
  currentPrototype: string;
  updateCurrentPrototype: Dispatch<SetStateAction<string>>;
}

export const AppContext = createContext<AppState | undefined>(undefined);

export const useAppContext = () => useContext(AppContext);

export const AppProvider = ({ children }) => {
  const [currentRunId, updateCurrentRunId] = useState(undefined);
  const [currentRunTree, updateCurrentRunTree] = useState(undefined);
  const [isLoading, updateIsLoading] = useState(false);
  const [isRunningSimulation, updateIsRunningSimulation] = useState(undefined);
  const [prototypes, updatePrototypes] = useState(undefined);
  const [currentPrototype, updateCurrentPrototype] = useState(undefined);

  return (
    <AppContext.Provider
      value={{
        isLoading,
        updateIsLoading,
        currentRunId,
        updateCurrentRunId,
        isRunningSimulation,
        updateIsRunningSimulation,
        currentRunTree,
        updateCurrentRunTree,
        prototypes,
        updatePrototypes,
        currentPrototype,
        updateCurrentPrototype,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};
