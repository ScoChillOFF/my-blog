import React from 'react'
import styles from './TextArea.module.css'

const TextArea = ({ jsonField, placeholder=null }) => {
  return (
    <textarea rows="5" className={styles.textArea} placeholder={placeholder} name={jsonField}></textarea>
  )
}

export default TextArea