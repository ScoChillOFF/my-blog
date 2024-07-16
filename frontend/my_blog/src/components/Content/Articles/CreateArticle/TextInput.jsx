import React from 'react'
import styles from './TextInput.module.css'

const TextInput = ({ jsonField, placeholder=null }) => {
  return (
    <input type="text" className={styles.textInput} name={jsonField} placeholder={placeholder} />
  )
}

export default TextInput