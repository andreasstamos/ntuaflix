import React from 'react'
import './Dropdown.css'


function Dropdown({order, setOrder, lang, menu}) {

  function handleOrderingChange(e) {
    setOrder(e.target.value);
  }
  return (
    <>
      <div className="select" htmlFor="slct">
        <label htmlFor="orderby">{lang === 'en' ? 'Order By:' : 'Ταξινόμηση κατά:'}    </label>
        <select id="slct" name="orderby" required="required" value={order} onChange={(e) => handleOrderingChange(e)}>
          <option value="" disabled="disabled">Select option</option>
          {menu.map((item, index) => {return <option key={index} value={item.value}>{lang === 'en' ? item.en : item.gr}</option>})}
          {/* <option value="1">{lang === 'en' ? 'Newest' : 'Πιο Πρόσφατα'}</option>
          <option value="2">{lang === 'en' ? 'Oldest' : 'Παλαιότερα'}</option>
          <option value="3">{lang === 'en' ? 'Ending Sooner' : 'Λήγουν Συντομότερα'}</option> */}
        </select>
        <svg>
          <use href="#select-arrow-down"></use>
        </svg>
      </div>
      <svg className="sprites">
        <symbol id="select-arrow-down" viewBox="0 0 10 6">
          <polyline points="1 1 5 5 9 1"></polyline>
        </symbol>
      </svg>
    </>
  )
}

export default Dropdown