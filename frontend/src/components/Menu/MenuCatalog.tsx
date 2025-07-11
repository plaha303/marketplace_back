import { Link } from "react-router";
import useCategoryQuery from "@/hooks/useCategoryQuery";
import { Category } from "@/utils/packages/categories/type/interfaces";


function MenuCatalog() {
  const {allCategories} = useCategoryQuery();

  const minSizeCol = 4;

  function columnsCategory(arr: Category[], sizeCol: number) {
    const result = [];

    for(let i = 0; i < arr.length; i+=sizeCol) {
      result.push(arr.slice(i, i + sizeCol))
    }

    return result;
  }

  const categoryCols = columnsCategory(allCategories?.results ?? [], minSizeCol);

  return (
    <div className="menu-catalog xl:absolute z-[99]">
      <div className="container mx-auto lg:px-4">
        <div className="menu-catalog__inner lg:shadow-custom1 lg:p-6 lg:rounded-sm bg-snow">
          <div className="xl:flex gap-6 flex-wrap">
            {categoryCols.map((col, i) => (
              <ul className="menu-catalog__items lg:min-w-[256px] lg:gap-y-0 gap-y-1 lg:block flex flex-col" key={i}>
                {col.map((item, _) => (
                  <li key={item.id}>
                    <Link to={`${item.category_href}`} className="menu-catalog__link text-size-body-3 flex items-center lg:p-3 py-1 px-4">
                      <span className="menu-catalog__icon lg:w-[48px] lg:h-[48px] w-10 h-10 mr-2 block rounded-full">
                        <img src={item.category_image} alt="" className="rounded-full h-full object-cover" />
                      </span>
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
              
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default MenuCatalog;