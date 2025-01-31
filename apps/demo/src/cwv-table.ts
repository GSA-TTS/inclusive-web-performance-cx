import { LitElement, html } from 'lit';
import { customElement, property } from 'lit/decorators.js';

@customElement('cwv-table')
export class CWVTable extends LitElement {
  @property() data?: Array<any>;

  async connectedCallback() {
    super.connectedCallback();
    const response = await fetch('http://localhost:5173/api/agency/gsa/all');
    this.data = await response.json();
    this.requestUpdate(); // Trigger re-render when data is ready
  }

  createRenderRoot() {
    return this;
  }

  render() {
    return this.data
      ? html`
          <table
            class="usa-table usa-table--stacked-header usa-table--borderless width-full cwv-table"
            slot="results-table"
          >
            <caption>
              Performance of GSA web properties
            </caption>
            <thead>
              <tr>
                <th scope="col">Origin</th>
                <th scope="col">
                  Passes <abbr title="Core Web Vitals">CWV</abbr>
                </th>
                <th scope="col">
                  % Good <abbr title="Largest Contentful Paint">LCP</abbr>
                  </span>
                </th>
                <th scope="col">
                  % Good <abbr title="Cumulative Layout Shift">CLS</abbr>
                </th>
                <th scope="col">
                  % Good <abbr title="Interaction to Next Paint">INP</abbr>
                </th>
              </tr>
            </thead>
            <tbody>
              ${this.data.map(
                item => html`
                  <tr>
                    <td data-label="Origin">${item.origin}</td>
                    <td data-label="Passes CWV">
                      ${typeof item.passes_cwv === 'boolean' &&
                      item.passes_cwv === true
                        ? html`
                            <span class="display-flex flex-align-center">
                              <svg
                                class="usa-icon margin-right-1 cwv-table__icon cwv-table__icon--pass"
                                aria-hidden="true"
                                role="img"
                              >
                                <use
                                  href="/uswds/img/sprite.svg#check_circle"
                                ></use>
                              </svg>
                              Yes
                            </span>
                          `
                        : html`
                            <span class="display-flex flex-align-center">
                              <svg
                                class="usa-icon margin-right-1 cwv-table__icon cwv-table__icon--fail"
                                aria-hidden="true"
                                role="img"
                              >
                                <use href="/uswds/img/sprite.svg#cancel"></use>
                              </svg>
                              No
                            </span>
                          `}
                    </td>
                    <td data-label="% Good Largest Contentful Paint">
                      ${item.largest_contentful_paint_good_density
                        ? html`
                            <cwv-percent
                              value=${item.largest_contentful_paint_good_density *
                              100}
                            >
                              ${(
                                item.largest_contentful_paint_good_density * 100
                              ).toFixed(2)}%
                            </cwv-percent>
                          `
                        : html`Not enough data`}
                    </td>
                    <td data-label="% Good Cumulative Layout Shift">
                      ${item.cumulative_layout_shift_good_density
                        ? html`
                            <cwv-percent
                              value=${item.cumulative_layout_shift_good_density *
                              100}
                            >
                              ${(
                                item.cumulative_layout_shift_good_density * 100
                              ).toFixed(2)}%
                            </cwv-percent>
                          `
                        : html`Not enough data`}
                    </td>
                    <td data-label="% Good Interaction to Next Paint">
                      ${item.interaction_to_next_paint_good_density
                        ? html`
                            <cwv-percent
                              value=${item.interaction_to_next_paint_good_density *
                              100}
                            >
                              ${(
                                item.interaction_to_next_paint_good_density *
                                100
                              ).toFixed(2)}%
                            </cwv-percent>
                          `
                        : html`Not enough data`}
                    </td>
                  </tr>
                `
              )}
            </tbody>
          </table>
<!--          <div class="cwv-table__footer bg-base-lightest padding-2">-->
<!--            <p><strong>About this data:</strong></p>-->
<!--            <ul>-->
<!--              <li>-->
<!--                To meet the passing criteria, LCP, CLS, and INP must all have a-->
<!--                &ldquo;Good&rdquo; percentage of 75% or greater.-->
<!--              </li>-->
<!--              <li>Good LCP values are 2.5s or less.</li>-->
<!--              <li>Good CLS values are 0.1 or less.</li>-->
<!--              <li>Good INP values are 200ms or less.</li>-->
<!--            </ul>-->
<!--          </div>-->
        `
      : html`<div>Loading...</div>`;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'cwv-table': CWVTable;
  }
}
