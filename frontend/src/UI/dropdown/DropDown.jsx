import styled from "./DropDown.module.css"

function DropDown({current, list, selectItem, classBlock}) {
  return (
    <div className="dropdown">
      <div tabIndex="0" role="button" className={`btn justify-between ${classBlock}`}>
        {current.toUpperCase()}
        <span className={`icon ${styled.arrow__down}`}></span>
      </div>
      <ul tabIndex="0" className="dropdown-content menu bg-base-100 rounded-box z-[1] w-full p-2 shadow">
        {list.map(item => (
            <li key={item.id} className={`${styled.dropdownContent__item} ${current === item.name ? styled.active : ''}`} >
              <a onClick={(e) => selectItem(item.name)} className="justify-center p-[8px] font-medium">{item.name.toUpperCase()}</a>
            </li>
          ))
        }
      </ul>
    </div>
  );
}

export default DropDown;