import React from "react";
import styles from "./TextInput.module.css";

const TextInput = ({
  jsonField,
  placeholder = null,
  onChange = () => {},
  value = "",
}) => {
  return (
    <input
      type="text"
      className={styles.textInput}
      name={jsonField}
      placeholder={placeholder}
      onChange={(Event) => onChange(Event.target.value)}
      value={value}
    />
  );
};

export default TextInput;
