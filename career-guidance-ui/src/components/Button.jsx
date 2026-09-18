const Button = ({ children, variant = 'primary', onClick, className = '', disabled = false, type = 'button' }) => {
  const baseStyles = 'px-6 py-2.5 rounded-md font-medium text-sm transition-all duration-150';
  
  const variants = {
    primary: 'bg-[#00cccc] text-black hover:bg-[#00b3b3]',
    secondary: 'border border-[#6b46c1] text-[#6b46c1] hover:bg-[#6b46c1] hover:text-white',
  };

  const disabledStyles = 'opacity-50 cursor-not-allowed';
  const enabledStyles = 'cursor-pointer';

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${disabled ? disabledStyles : enabledStyles} ${className}`}
      onClick={onClick}
      disabled={disabled}
      type={type}
    >
      {children}
    </button>
  );
};

export default Button;
