import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';

/**
 * An example element.
 *
 * @slot - This element has a slot
 * @csspart button - The button
 */
@customElement('cwv-bar-graph')
export class CWVBarGraph extends LitElement {
  @property() value: number = 0;

  static styles = css`
    :host {
      display: block;
    }

    .bar {
      display: block;
      background: none;
    }
  `;

  // protected updated(changed): void {
  //   if (changed.has('value') && !!this.value) {
  //     console.log(this.value);
  //     this.style.setProperty(
  //       'background'
  //     ); /* Set the value of the variable based on class property */
  //   }
  // }

  protected updated(changed): void {
    if (changed.has('value') && !!this.value) {
      console.log(this.value);

      // Calculate cleanValue (capping the value to a maximum of 100 for safety)
      const cleanValue = Math.min(this.value, 100);

      // Set the linear gradient as the background
      this.style.setProperty(
        'background',
        `linear-gradient(90deg, #e6e6e6 0%, #e6e6e6 ${cleanValue}%, transparent ${cleanValue}%)`
      );
    }
  }

  render() {
    return html`
      <span class="bar">
        <slot></slot>
      </span>
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'cwv-bar-graph': CWVBarGraph;
  }
}
