import React from 'react'
import styles from './Button.module.css'

const Button = ({ onClick, text, disabled=false }) => {
  return (
    <button className={styles.button} onClick={onClick} disabled={disabled}>{text}</button>
  )
}

export default Button