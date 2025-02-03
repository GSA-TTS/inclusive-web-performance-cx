import { LitElement, html } from 'lit';
import { customElement, property } from 'lit/decorators.js';

@customElement('cwv-table')
export class CWVTable extends LitElement {
  @property() data?: Array<any>;
  @property() filteredData?: Array<any>;

  endpointUrl = 'http://localhost:5173/api/agency/gsa';

  async connectedCallback() {
    super.connectedCallback();
    const response = await fetch(`${this.endpointUrl}/all`);
    this.data = await response.json();
    this.filteredData = this.data;
    this.requestUpdate(); // Trigger re-render when data is ready
  }

  _filterByPassStatus(status: boolean | null) {
    this.filteredData = this.data.filter(item => {
      if (status === null) {
        return true;
      }
      return item.passes_cwv === status;
    });
  }

  _filterByDevice(status: boolean | null) {
    console.log(status);
  }

  // Use the light dom to take advantage of the site's CSS
  createRenderRoot() {
    return this;
  }

  scorecardHtml() {
    const pass = this.data.filter(item => {
      return item.passes_cwv === true;
    }).length;

    const eligibleTotal = this.data.filter(
      item => item.passes_cwv !== null
    ).length;

    const fail = eligibleTotal - pass;
    const total = this.data.length;
    const passPercent = (pass / eligibleTotal) * 100;

    return html`
      <ul class="usa-card-group margin-bottom-0 margin-top-2">
        <li
          class="usa-card card:grid-col-12 tablet:grid-col-6 desktop:grid-col-4 card:padding-bottom-2 desktop:padding-bottom-0"
        >
          <div
            class="usa-card__container border-0 padding-2 bg-accent-cool-light"
          >
            <div class="usa-card__body text-center">
              <p class="margin-0">Core Web Vitals pass rate</p>
              <p class="font-sans-3xl margin-0 line-height-ui-3">
                <strong>${passPercent.toFixed(2)}%</strong>
              </p>
            </div>
          </div>
        </li>
        <li
          class="usa-card card:grid-col-12 tablet:grid-col-6 desktop:grid-col-8 card:padding-bottom-2 desktop:padding-bottom-0"
        >
          <div class="usa-card__container border-0 padding-2">
            <div class="usa-card__body">
              <p class="margin-bottom-0 font-body-lg">
                ${pass} of ${eligibleTotal} sites pass CWV. There were ${fail}
                sites that did not pass CWV and ${total - eligibleTotal} sites
                that didn't have enough data to calculate.
              </p>
            </div>
          </div>
        </li>
      </ul>
    `;
  }

  passesCWVHtml(value) {
    let message;

    if (value === true) {
      message = html`
        <span class="display-flex flex-align-center">
          <svg
            class="usa-icon margin-right-1 cwv-table__icon cwv-table__icon--pass"
            aria-hidden="true"
            role="img"
          >
            <use href="/uswds/img/sprite.svg#check_circle"></use></svg
          >Yes
        </span>
      `;
    } else if (value === false) {
      message = html`
        <span class="display-flex flex-align-center">
          <svg
            class="usa-icon margin-right-1 cwv-table__icon cwv-table__icon--fail"
            aria-hidden="true"
            role="img"
          >
            <use href="/uswds/img/sprite.svg#cancel"></use></svg
          >No</span
        >
      `;
    } else {
      message = html`
        <span class="display-flex flex-align-center">
          <svg
            class="usa-icon margin-right-1 cwv-table__icon cwv-table__icon--no-data"
            aria-hidden="true"
            role="img"
          >
            <use href="/uswds/img/sprite.svg#warning"></use></svg
          >Not Enough Data</span
        >
      `;
    }

    return message;
  }

  render() {
    return this.filteredData
      ? html`
        <div>
          ${this.scorecardHtml()}
        </div>
        <div class="grid-row">
          <div class="tablet:grid-col-6">
            <p><strong>Filter by CWV status:</strong></p>
            <div class="usa-button-group">
              <button class="usa-button" @click="${() => this._filterByPassStatus(null)}">Show all</button>
              <button class="usa-button" @click="${() => this._filterByPassStatus(true)}">Yes</button>
              <button class="usa-button" @click="${() => this._filterByPassStatus(false)}">No</button>
            </div>
          </div>
          <div class="tablet:grid-col-6">
            <p><strong>Filter by device:</strong></p>
            <div class="usa-button-group">
              <button class="usa-button" @click="${() => this._filterByDevice(null)}">Show all</button>
              <button class="usa-button" @click="${() => this._filterByDevice('phone')}">Phone</button>
              <button class="usa-button" @click="${() => this._filterByDevice('desktop')}">Desktop</button>
            </div>
          </div>
        </div>

        <table
          class="usa-table usa-table--stacked-header usa-table--borderless width-full cwv-table"
          slot="results-table"
        >
          <caption>
            Page speed details for GSA web properties
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
            ${this.filteredData.map(
              item => html`
                <tr>
                  <td data-label="Origin">${item.origin}</td>
                  <td data-label="Passes CWV">
                    ${this.passesCWVHtml(item.passes_cwv)}
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
                      : html`<span aria-hidden="true">-</span>`}
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
                      : html`<span aria-hidden="true">-</span>`}
                  </td>
                  <td data-label="% Good Interaction to Next Paint">
                    ${item.interaction_to_next_paint_good_density
                      ? html`
                          <cwv-percent
                            value=${item.interaction_to_next_paint_good_density *
                            100}
                          >
                            ${(
                              item.interaction_to_next_paint_good_density * 100
                            ).toFixed(2)}%
                          </cwv-percent>
                        `
                      : html`<span aria-hidden="true">-</span>`}
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
