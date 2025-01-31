import { LitElement, html } from 'lit';
import { customElement, property } from 'lit/decorators.js';

/**
 * An example element.
 *
 * @slot - This element has a slot
 * @csspart button - The button
 */
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
            class="usa-table usa-table--stacked-header usa-table--borderless width-full"
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
                  <span
                    class="usa-tooltip"
                    title="To meet the passing criteria, LCP, CLS, and INP must all have a &ldquo;Good&rdquo; percentage of 75% or greater."
                  >
                    <svg class="usa-icon" aria-labelledby="cwv-info" role="img">
                      <title id="cwv-info">About Passing CWV</title>
                      <use href="/uswds/img/sprite.svg#info"></use>
                    </svg>
                  </span>
                </th>
                <th scope="col">
                  % Good <abbr title="Largest Contentful Paint">LCP</abbr>
                  <span
                    class="usa-tooltip"
                    title="Good LCP values are 2.5s or less."
                  >
                    <svg class="usa-icon" aria-labelledby="lcp-info" role="img">
                      <title id="lcp-info">What is a Good LCP?</title>
                      <use href="/uswds/img/sprite.svg#info"></use>
                    </svg>
                  </span>
                </th>
                <th scope="col">
                  % Good <abbr title="Cumulative Layout Shift">CLS</abbr>
                  <span
                    class="usa-tooltip"
                    title="Good CLS values are 0.1 or less."
                  >
                    <svg class="usa-icon" aria-labelledby="cls-info" role="img">
                      <title id="cls-info">What is a Good CLS?</title>
                      <use href="/uswds/img/sprite.svg#info"></use>
                    </svg>
                  </span>
                </th>
                <th scope="col">
                  % Good <abbr title="Interaction to Next Paint">INP</abbr>
                  <span
                    class="usa-tooltip"
                    title="Good INP values are 200ms or less."
                  >
                    <svg class="usa-icon" aria-labelledby="inp-info" role="img">
                      <title id="inp-info">What is a Good INP?</title>
                      <use href="/uswds/img/sprite.svg#info"></use>
                    </svg>
                  </span>
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
                            ${(
                              item.largest_contentful_paint_good_density * 100
                            ).toFixed(2)}%
                          `
                        : html`Not enough data`}
                    </td>
                    <td data-label="% Good Cumulative Layout Shift">
                      ${item.cumulative_layout_shift_good_density
                        ? html`
                            ${(
                              item.cumulative_layout_shift_good_density * 100
                            ).toFixed(2)}%
                          `
                        : html`Not enough data`}
                    </td>
                    <td data-label="% Good Interaction to Next Paint">
                      ${item.interaction_to_next_paint_good_density
                        ? html`
                            ${(
                              item.interaction_to_next_paint_good_density * 100
                            ).toFixed(2)}%
                          `
                        : html`Not enough data`}
                    </td>
                  </tr>
                `
              )}
            </tbody>
          </table>
        `
      : html`<div>Loading...</div>`;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'cwv-table': CWVTable;
  }
}
