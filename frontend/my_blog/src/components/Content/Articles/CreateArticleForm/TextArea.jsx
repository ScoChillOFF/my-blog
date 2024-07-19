import React from "react";
import styles from "./TextArea.module.css";

const TextArea = ({
  jsonField,
  placeholder = null,
  value = "",
  onChange = () => {},
}) => {
  return (
    <textarea
      rows="5"
      className={styles.textArea}
      placeholder={placeholder}
      name={jsonField}
      value={value}
      onChange={(Event) => onChange(Event.currentTarget.value)}
    ></textarea>
  );
};

export default TextArea;
