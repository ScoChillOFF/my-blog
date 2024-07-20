import React, { useState } from "react";
import styles from "./CheckboxInput.module.css"

const CheckboxInput = ({ label, name, value, onChange }) => {
  const [isChecked, setIsChecked] = useState(false);

  async function handleChange() {
    setIsChecked(!isChecked);
    await onChange();
  }

  return (
    <label className={styles.checkbox}>
      <input
        type="checkbox"
        name={name}
        value={value}
        checked={isChecked}
        onChange={handleChange}
        />
      {label}
    </label>
  );
};

export default CheckboxInput;
