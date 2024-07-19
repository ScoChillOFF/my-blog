import React from "react";
import styles from "./RadioInput.module.css"

const RadioInput = ({ label, name, value, selectedValue, onChange }) => {
  return (
      <label className={styles.radio} htmlFor="">
        <input
          type="radio"
          name={name}
          value={value}
          onChange={(Event) => onChange(Event.currentTarget.value)}
          selected={value == selectedValue}
        />
        {label}
      </label>
  );
};

export default RadioInput;
